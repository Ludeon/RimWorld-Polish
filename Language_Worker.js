public class LanguageWorker_Polish : LanguageWorker
	{
		public override string WithIndefiniteArticle(string str, Gender gender, bool plural = false, bool name = false)
		{
			return str;
		}

		public override string WithDefiniteArticle(string str, Gender gender, bool plural = false, bool name = false)
		{
			return str;
		}

		private interface IResolver
		{
			string Resolve(string[] arguments);
		}

		private class ReplaceResolver : IResolver
		{
			// ^Replace('{0}', 'jeden-jedna')^
			private static readonly Regex _argumentRegex =
				new Regex(@"'(?<old>[^']*?)'-'(?<new>[^']*?)'", RegexOptions.Compiled);

			public string Resolve(string[] arguments)
			{
				if (arguments.Length == 0)
				{
					return null;
				}

				string input = arguments[0];

				if (arguments.Length == 1)
				{
					return input;
				}

				for (int i = 1; i < arguments.Length; ++i)
				{
					string argument = arguments[i];

					Match match = _argumentRegex.Match(argument);
					if (!match.Success)
					{
						return null;
					}

					string oldValue = match.Groups["old"].Value;
					string newValue = match.Groups["new"].Value;

					if (oldValue == input)
					{
						return newValue;
					}

					//Log.Message(string.Format("input: {0}, old: {1}, new: {2}", input, oldGroup.Captures[i].Value, newGroup.Captures[i].Value));
				}

				return input;
			}
		}

		private class NumberCaseResolver : IResolver
		{
			// ^Number( {0} | '# komentarz' | '# komentarze' | '# komentarzy' | '# komentarza' )^
			// ^Number( {0} | '1           | 2              | 10              | 1/2            )^
			private static readonly Regex _numberRegex =
				new Regex(@"(?<floor>[0-9]+)(\.(?<frac>[0-9]+))?", RegexOptions.Compiled);

			public string Resolve(string[] arguments)
			{
				if (arguments.Length != 5)
				{
					return null;
				}

				string numberStr = arguments[0];
				Match numberMatch = _numberRegex.Match(numberStr);
				if (!numberMatch.Success)
				{
					return null;
				}

				bool hasFracPart = numberMatch.Groups["frac"].Success;

				string floorStr = numberMatch.Groups["floor"].Value;

				string formOne = arguments[1].Trim('\'');
				string formSeveral = arguments[2].Trim('\'');
				string formMany = arguments[3].Trim('\'');
				string fraction = arguments[4].Trim('\'');

				if (hasFracPart)
				{
					return fraction.Replace("#", numberStr);
				}

				int floor = int.Parse(floorStr);
				return GetFormForNumber(floor, formOne, formSeveral, formMany).Replace("#", numberStr);
			}

			private static string GetFormForNumber(int number, string formOne, string formSeveral, string formMany)
			{
				if (number == 1)
				{
					return formOne;
				}

				if (number % 10 >= 2 && number % 10 <= 4 && (number % 100 < 10 || number % 100 >= 20))
				{
					return formSeveral;
				}

				return formMany;
			}
		}

		private static readonly ReplaceResolver replaceResolver = new ReplaceResolver();
		private static readonly NumberCaseResolver numberCaseResolver = new NumberCaseResolver();

		private static readonly Regex _languageWorkerResolverRegex =
			new Regex(@"\^(?<resolverName>\w+)\(\s*(?<argument>[^|]+?)\s*(\|\s*(?<argument>[^|]+?)\s*)*\)\^",
				RegexOptions.Compiled);

		public override string PostProcessedKeyedTranslation(string translation)
		{
			translation = base.PostProcessedKeyedTranslation(translation);
			return PostProcess(translation);
		}

		public override string PostProcessed(string str)
		{
			str = base.PostProcessed(str);
			return PostProcess(str);
		}

		private static string PostProcess(string translation)
		{
			return _languageWorkerResolverRegex.Replace(translation, EvaluateResolver);
		}

		private static string EvaluateResolver(Match match)
		{
			string keyword = match.Groups["resolverName"].Value;

			Group argumentsGroup = match.Groups["argument"];

			string[] arguments = new string[argumentsGroup.Captures.Count];
			for (int i = 0; i < argumentsGroup.Captures.Count; ++i)
			{
				arguments[i] = argumentsGroup.Captures[i].Value.Trim();
			}

			IResolver resolver = GetResolverByKeyword(keyword);

			string result = resolver.Resolve(arguments);
			if (result == null)
			{
				Log.Error(string.Format("Error happened while resolving LW instruction: \"{0}\"", match.Value));
				return match.Value;
			}

			return result;
		}

		private static IResolver GetResolverByKeyword(string keyword)
		{
			switch (keyword)
			{
				case "Replace":
					return replaceResolver;
				case "Number":
					return numberCaseResolver;
				default:
					return null;
			}
		}
	}